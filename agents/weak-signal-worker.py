#!/usr/bin/env python3
"""
Weak Signal Worker: Bridge between WeakSignalFinder and PCA Capture pipeline.

Polls WeakSignalFinder output, normalizes signals, detects novelty,
and feeds into Capture Worker for validation and routing.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
import hashlib
import logging
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class NoveltyIndicators:
    """Signal novelty and urgency metrics."""
    trend_novelty: float
    trend_urgency: float
    semantic_density: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


@dataclass
class QualityMetrics:
    """Signal quality assessment."""
    data_completeness: float
    language_detection: float
    trend_confidence: float
    deduplication_check: str = "passed"

    def to_dict(self) -> Dict:
        return asdict(self)


class SignalDeduplicator:
    """Maintains history and detects duplicate signals."""

    def __init__(self, window_days: int = 30, similarity_threshold: float = 0.85):
        self.window_days = window_days
        self.similarity_threshold = similarity_threshold
        self.history: List[Dict[str, Any]] = []

    def add_signal(self, signal_hash: str, topics: List[str]) -> None:
        """Add signal to history."""
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "hash": signal_hash,
            "topics": set(topics)
        })
        self._prune_old_signals()

    def _prune_old_signals(self) -> None:
        """Remove signals older than window."""
        cutoff = datetime.utcnow() - timedelta(days=self.window_days)
        self.history = [
            s for s in self.history
            if datetime.fromisoformat(s["timestamp"]) > cutoff
        ]

    def is_duplicate(self, topics: List[str]) -> bool:
        """Check if signal is duplicate of recent signals."""
        current_set = set(topics[:10])  # Top 10 topics only

        for past_signal in self.history:
            past_set = past_signal["topics"]
            if len(past_set) == 0 or len(current_set) == 0:
                continue

            # Calculate Jaccard similarity
            intersection = len(current_set & past_set)
            union = len(current_set | past_set)
            similarity = intersection / union if union > 0 else 0

            if similarity > self.similarity_threshold:
                logger.info(
                    f"Duplicate detected (similarity={similarity:.2f}), "
                    f"skipping this signal"
                )
                return True

        return False


class WeakSignalWorker:
    """
    Processes WeakSignalFinder output and normalizes into PCA Capture schema.
    """

    def __init__(
        self,
        wsf_output_dir: str = "./external/weak-signal-finder/dataset",
        novelty_threshold: float = 0.75,
        top_words_to_extract: int = 20,
        min_completeness: float = 0.90,
        dedup_window_days: int = 30,
    ):
        self.wsf_output_dir = Path(wsf_output_dir)
        self.novelty_threshold = novelty_threshold
        self.top_words_to_extract = top_words_to_extract
        self.min_completeness = min_completeness
        self.deduplicator = SignalDeduplicator(
            window_days=dedup_window_days,
            similarity_threshold=0.85
        )

        logger.info(f"Initialized WeakSignalWorker (output_dir={wsf_output_dir})")

    def poll_latest_signal(self) -> Optional[Dict[str, Any]]:
        """
        Detect and return the latest unprocessed signal file.

        Returns None if no new files found.
        """
        if not self.wsf_output_dir.exists():
            logger.error(f"Output directory does not exist: {self.wsf_output_dir}")
            return None

        json_files = sorted(
            self.wsf_output_dir.glob("signals_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        if not json_files:
            logger.info("No signal files found in output directory")
            return None

        latest_file = json_files[0]
        age_minutes = (datetime.utcnow().timestamp() - latest_file.stat().st_mtime) / 60

        if age_minutes > 120:  # 2 hours
            logger.warning(
                f"Latest signal file is {age_minutes:.0f} minutes old, "
                "WeakSignalFinder may not be running"
            )

        try:
            with open(latest_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to parse signal file {latest_file}: {e}")
            return None

    def extract_trending_topics(self, wsf_data: Dict) -> List[Dict[str, Any]]:
        """
        Extract top trending topics from WeakSignalFinder output.
        """
        top_words = wsf_data.get("topWords", [])

        if not top_words:
            logger.warning("No top words found in signal data")
            return []

        topics = []
        for item in top_words[:self.top_words_to_extract]:
            topics.append({
                "topic": item.get("word", ""),
                "frequency": item.get("frequency", 0),
                "novelty_score": item.get("novelty", 0.5),
                "confidence": item.get("score", 0.8),
                "category": item.get("category", "general")
            })

        return topics

    def extract_semantic_clusters(self, wsf_data: Dict) -> List[Dict[str, Any]]:
        """
        Extract semantic neighborhoods (word clusters) from WeakSignalFinder.
        """
        neighborhoods = wsf_data.get("semanticNeighborhoods", [])

        clusters = []
        for item in neighborhoods:
            clusters.append({
                "hub": item.get("hub", ""),
                "cluster_size": len(item.get("neighbors", [])),
                "cluster_strength": item.get("strength", 0.5),
                "neighbors": item.get("neighbors", [])
            })

        return clusters

    def calculate_novelty_indicators(
        self,
        topics: List[Dict[str, Any]],
        coverage_count: int
    ) -> NoveltyIndicators:
        """
        Calculate novelty, urgency, and semantic density scores.
        """
        if not topics:
            return NoveltyIndicators(
                trend_novelty=0.0,
                trend_urgency=0.0,
                semantic_density=0.0
            )

        # Novelty: average novelty score of top topics
        novelty_scores = [t.get("novelty_score", 0.5) for t in topics[:5]]
        trend_novelty = sum(novelty_scores) / len(novelty_scores) if novelty_scores else 0.5

        # Urgency: based on coverage volume and top-topic frequency
        urgency = min(1.0, coverage_count / 500)  # Normalize to 0-1 range

        # Semantic density: how tightly clustered are the trends?
        # (This would be more sophisticated with full semantic analysis)
        semantic_density = sum(t.get("confidence", 0.5) for t in topics[:5]) / 5 if topics else 0.5

        return NoveltyIndicators(
            trend_novelty=trend_novelty,
            trend_urgency=urgency,
            semantic_density=semantic_density
        )

    def validate_quality(self, wsf_data: Dict, topics: List[Dict]) -> QualityMetrics:
        """
        Assess data quality and confidence.
        """
        sources = wsf_data.get("sources", {})
        article_count = sources.get("count", 0)
        languages = sources.get("languages", [])

        # Completeness: do we have the expected data?
        has_top_words = "topWords" in wsf_data and len(wsf_data["topWords"]) > 0
        has_neighborhoods = "semanticNeighborhoods" in wsf_data
        has_sources = "sources" in wsf_data
        completeness = sum([has_top_words, has_neighborhoods, has_sources]) / 3

        # Language detection confidence (assume spaCy handled this well)
        language_confidence = 0.99 if languages else 0.70

        # Trend confidence based on article count
        trend_confidence = min(
            1.0,
            max(0.5, article_count / 500)
        )

        return QualityMetrics(
            data_completeness=completeness,
            language_detection=language_confidence,
            trend_confidence=trend_confidence
        )

    def normalize_to_capture_schema(
        self,
        wsf_data: Dict,
        capture_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Transform WeakSignalFinder output into PCA Capture schema.
        """
        timestamp = wsf_data.get("timestamp", datetime.utcnow().isoformat())
        sources = wsf_data.get("sources", {})

        # Extract components
        topics = self.extract_trending_topics(wsf_data)
        clusters = self.extract_semantic_clusters(wsf_data)

        # Check for duplicates
        topic_names = [t["topic"] for t in topics]
        if self.deduplicator.is_duplicate(topic_names):
            logger.info(f"Signal {capture_id} is duplicate, skipping")
            return None

        # Validate quality
        quality = self.validate_quality(wsf_data, topics)
        if quality.data_completeness < self.min_completeness:
            logger.warning(
                f"Signal {capture_id} below quality threshold "
                f"(completeness={quality.data_completeness:.2f})"
            )

        # Calculate novelty
        novelty = self.calculate_novelty_indicators(
            topics,
            sources.get("count", 0)
        )

        # Build summary text
        summary_lines = ["**Emerging Trends from RSS Monitoring**\n"]
        summary_lines.append(f"Detected from {sources.get('count', 0)} articles across {len(sources.get('languages', []))} languages.\n")
        summary_lines.append("\n**Top Trending Topics:**\n")
        for topic in topics[:10]:
            summary_lines.append(
                f"- {topic['topic'].title()}: "
                f"frequency={topic['frequency']}, "
                f"novelty={topic['novelty_score']:.2f}\n"
            )

        # Build capture document
        capture = {
            "capture_id": capture_id,
            "source_type": "rss-signal",
            "source_system": "weak-signal-finder",
            "content_type": "signal-trends",
            "timestamp": timestamp,
            "normalized_text": "".join(summary_lines),
            "metadata": {
                "signal_type": "trend-emergence",
                "trending_topics": topics,
                "semantic_clusters": clusters,
                "coverage": {
                    "article_count": sources.get("count", 0),
                    "languages": sources.get("languages", []),
                    "regions": sources.get("regions", ["global"]),
                    "feed_count": sources.get("feed_count", 0)
                },
                "signal_indicators": novelty.to_dict()
            },
            "quality_metrics": quality.to_dict()
        }

        return capture

    def process_signal(self) -> Optional[Dict[str, Any]]:
        """
        Main processing pipeline: poll, validate, normalize, deduplicate.

        Returns normalized capture document or None if skipped.
        """
        # Poll for new signal
        wsf_data = self.poll_latest_signal()
        if not wsf_data:
            return None

        # Generate capture ID
        capture_id = f"signal-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        logger.info(f"Processing signal: {capture_id}")

        try:
            # Normalize to capture schema
            capture = self.normalize_to_capture_schema(wsf_data, capture_id)

            if capture:
                # Record in deduplicator
                topic_names = [
                    t["topic"] for t in capture["metadata"]["trending_topics"]
                ]
                signal_hash = hashlib.md5(
                    json.dumps(sorted(topic_names)).encode()
                ).hexdigest()
                self.deduplicator.add_signal(signal_hash, topic_names)

                logger.info(
                    f"Signal {capture_id} processed successfully "
                    f"(novelty={capture['metadata']['signal_indicators']['trend_novelty']:.2f})"
                )
                return capture
            else:
                logger.info(f"Signal {capture_id} was deduplicated or invalid")
                return None

        except Exception as e:
            logger.error(f"Error processing signal {capture_id}: {e}", exc_info=True)
            return None


def main():
    """Demo: process a single signal."""
    worker = WeakSignalWorker(
        wsf_output_dir=os.getenv(
            "WSF_OUTPUT_DIR",
            "./external/weak-signal-finder/dataset"
        )
    )

    capture = worker.process_signal()
    if capture:
        print(json.dumps(capture, indent=2))
        print("\n✓ Signal normalized and ready for Capture Worker")
    else:
        print("No signal to process")


if __name__ == "__main__":
    main()
