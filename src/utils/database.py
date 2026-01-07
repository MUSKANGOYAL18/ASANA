"""Database utilities for SQLite operations."""
import sqlite3
import json
from pathlib import Path
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class Database:
    """SQLite database manager."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Establish database connection."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        logger.info(f"Connected to database: {self.db_path}")
        
    def initialize_schema(self, schema_path: str):
        """Initialize database schema from SQL file."""
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        self.conn.executescript(schema_sql)
        self.conn.commit()
        logger.info("Database schema initialized")
        
    def insert(self, table: str, data: Dict[str, Any]):
        """Insert a single row into a table."""
        # Convert datetime objects to ISO format strings
        processed_data = {}
        for key, value in data.items():
            if hasattr(value, 'isoformat'):
                processed_data[key] = value.isoformat()
            elif isinstance(value, (dict, list)):
                processed_data[key] = json.dumps(value)
            else:
                processed_data[key] = value
        
        columns = ', '.join(processed_data.keys())
        placeholders = ', '.join(['?' for _ in processed_data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            self.conn.execute(query, list(processed_data.values()))
        except sqlite3.IntegrityError as e:
            logger.warning(f"Integrity error inserting into {table}: {e}")
            raise
            
    def insert_many(self, table: str, data_list: List[Dict[str, Any]]):
        """Insert multiple rows into a table."""
        if not data_list:
            return
            
        for data in data_list:
            self.insert(table, data)
        
        self.conn.commit()
        logger.info(f"Inserted {len(data_list)} rows into {table}")
        
    def query(self, sql: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a SELECT query."""
        cursor = self.conn.execute(sql, params)
        return cursor.fetchall()
        
    def commit(self):
        """Commit current transaction."""
        self.conn.commit()
        
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
            
    def get_stats(self) -> Dict[str, int]:
        """Get row counts for all tables."""
        tables = [
            'organizations', 'teams', 'users', 'team_memberships',
            'projects', 'sections', 'tasks', 'comments',
            'custom_field_definitions', 'custom_field_values',
            'tags', 'task_tags', 'attachments'
        ]
        
        stats = {}
        for table in tables:
            result = self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            stats[table] = result[0]
            
        return stats