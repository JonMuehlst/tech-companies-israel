from typing import List, Optional

from sqlalchemy.orm import Session

from tci.db.models import Job
from tci.db.postgresql import db


class JobService:
    def __init__(self):
        self.db = db

    def get_jobs(self, limit: int = 100, offset: int = 0) -> List[Job]:
        """Get a list of jobs with pagination"""
        with self.db.get_session() as session:
            return session.query(Job).offset(offset).limit(limit).all()

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """Get a job by its ID"""
        with self.db.get_session() as session:
            return session.query(Job).filter(Job.id == job_id).first()

    def search_jobs(self, query: str, limit: int = 100) -> List[Job]:
        """Search jobs by title or description"""
        with self.db.get_session() as session:
            return (
                session.query(Job)
                .filter(
                    (Job.title.ilike(f"%{query}%"))
                    | (Job.description.ilike(f"%{query}%"))
                )
                .limit(limit)
                .all()
            )


job_service = JobService()
