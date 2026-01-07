"""Temporal utilities for date/time generation with consistency."""
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
import numpy as np


class TemporalGenerator:
    """Generate temporally consistent dates and times."""

    def __init__(self, start_date: datetime, end_date: datetime, seed: int = 42):
        self.start_date = start_date
        self.end_date = end_date
        self.rng = np.random.RandomState(seed)

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    def random_date_in_range(self, start_date: datetime, end_date: datetime) -> datetime:
        """
        Return a random date between start_date and end_date (inclusive).
        If the range is invalid, safely return start_date.
        """
        if not start_date or not end_date:
            return start_date

        if end_date <= start_date:
            return start_date  # HARD SAFETY GUARD

        delta = end_date - start_date
        max_days = max(delta.days, 0)

        random_days = self.rng.randint(0, max_days + 1)
        return start_date + timedelta(days=random_days)

    # ------------------------------------------------------------------

    def random_business_date(
        self,
        start: datetime,
        end: datetime,
        avoid_weekends: bool = True
    ) -> datetime:
        """Generate random date, optionally avoiding weekends."""
        date = self.random_date_in_range(start, end)

        if avoid_weekends and self.rng.random() < 0.85:
            # Push forward to next weekday if needed
            while date.weekday() >= 5:
                date += timedelta(days=1)

            # Never exceed simulation end
            if date > self.end_date:
                date = self.end_date

        return date

    # ------------------------------------------------------------------
    # Due dates
    # ------------------------------------------------------------------

    def generate_due_date(
        self,
        created_at: datetime,
        distribution: dict
    ) -> Optional[datetime]:
        """
        Generate due date based on research-backed distribution.

        Distribution (Asana / Atlassian-inspired):
        - no_due_date
        - overdue
        - within_1_week
        - within_1_month
        - within_1_3_months
        """
        r = self.rng.random()

        if r < distribution["no_due_date"]:
            return None

        r -= distribution["no_due_date"]

        if r < distribution["overdue"]:
            # Overdue: 1–30 days before creation
            return created_at - timedelta(days=self.rng.randint(1, 31))

        r -= distribution["overdue"]

        if r < distribution["within_1_week"]:
            return self.random_business_date(
                created_at,
                created_at + timedelta(days=self.rng.randint(1, 8))
            )

        r -= distribution["within_1_week"]

        if r < distribution["within_1_month"]:
            return self.random_business_date(
                created_at,
                created_at + timedelta(days=self.rng.randint(8, 31))
            )

        # 1–3 months
        return self.random_business_date(
            created_at,
            created_at + timedelta(days=self.rng.randint(31, 91))
        )

    # ------------------------------------------------------------------
    # Completion times
    # ------------------------------------------------------------------

    def generate_completion_time(
        self,
        created_at: datetime,
        due_date: Optional[datetime] = None
    ) -> datetime:
        """
        Generate task completion time.

        Properties:
        - Always >= created_at
        - Never > simulation end_date
        - Some tasks complete late
        """

        # Log-normal cycle time (enterprise realistic)
        mu = 1.5     # ~4–5 days median
        sigma = 0.8  # long tail

        days_to_complete = min(self.rng.lognormal(mu, sigma), 30)
        completed_at = created_at + timedelta(days=days_to_complete)

        # Clamp to simulation end
        if completed_at > self.end_date:
            completed_at = self.random_date_in_range(created_at, self.end_date)

        # Late completion logic (CORRECTED)
        if due_date and completed_at > due_date:
            # 30% tasks finish late
            if self.rng.random() < 0.30:
                late_days = self.rng.randint(1, 8)
                completed_at = due_date + timedelta(days=late_days)

                # Clamp again
                if completed_at > self.end_date:
                    completed_at = self.end_date

        # Absolute safety
        if completed_at < created_at:
            completed_at = created_at

        return completed_at

    # ------------------------------------------------------------------
    # Time-of-day
    # ------------------------------------------------------------------

    def generate_workday_time(self, date: datetime) -> datetime:
        """Generate time during work hours (9 AM – 6 PM)."""
        hour = self.rng.randint(9, 19)
        minute = self.rng.randint(0, 60)

        return date.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

    # ------------------------------------------------------------------
    # Sprints
    # ------------------------------------------------------------------

    def generate_sprint_dates(
        self,
        start: datetime,
        num_sprints: int = 12
    ) -> List[Tuple[datetime, datetime]]:
        """
        Generate 2-week sprint boundaries.
        """
        sprints = []
        current = start

        for _ in range(num_sprints):
            sprint_start = current
            sprint_end = current + timedelta(days=14)

            if sprint_start > self.end_date:
                break

            sprints.append((
                sprint_start,
                min(sprint_end, self.end_date)
            ))
            current = sprint_end

        return sprints
