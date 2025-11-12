"""
Vector-based memory for semantic search and retrieval of past campaigns.
Uses ChromaDB for vector storage and similarity search.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import json

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("Warning: chromadb not installed. Vector memory will be disabled.")
    print("Install with: pip install chromadb")


class VectorMemory:
    """Vector-based memory for semantic search and retrieval."""
    
    def __init__(self, collection_name: str = "campaign_memory", persist_directory: Optional[str] = None):
        """
        Initialize vector memory with ChromaDB.
        
        Args:
            collection_name: Name of the collection to store campaigns
            persist_directory: Optional directory to persist the database
        """
        if not CHROMA_AVAILABLE:
            self.available = False
            self.client = None
            self.collection = None
            return
        
        self.available = True
        try:
            if persist_directory:
                self.client = chromadb.PersistentClient(path=persist_directory)
            else:
                self.client = chromadb.Client(Settings(anonymized_telemetry=False))
            
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Campaign memory storage for semantic search"}
            )
        except Exception as e:
            print(f"Warning: Could not initialize vector memory: {e}")
            self.available = False
            self.client = None
            self.collection = None
    
    def store_campaign(self, campaign_id: str, brief: str, output: Dict[str, Any], metadata: Dict[str, Any] = None):
        """
        Store campaign in vector database for future retrieval.
        
        Args:
            campaign_id: Unique identifier for the campaign
            brief: Campaign brief text
            output: Campaign output dictionary
            metadata: Additional metadata to store
        """
        if not self.available or not self.collection:
            return False
        
        try:
            # Combine text for embedding (the more context, the better the search)
            text_parts = [f"Brief: {brief}"]
            
            # Add key output information
            if isinstance(output, dict):
                if output.get("target_audience"):
                    text_parts.append(f"Target Audience: {output['target_audience']}")
                if output.get("core_message"):
                    text_parts.append(f"Core Message: {output['core_message']}")
                if output.get("strategy"):
                    text_parts.append(f"Strategy: {output['strategy']}")
                if output.get("recommended_channels"):
                    channels = output['recommended_channels']
                    if isinstance(channels, list):
                        text_parts.append(f"Channels: {', '.join(channels)}")
                    else:
                        text_parts.append(f"Channels: {channels}")
            
            text = " | ".join(text_parts)
            
            # Prepare metadata
            meta = {
                "brief": brief,
                "timestamp": datetime.now().isoformat(),
                "campaign_id": campaign_id,
            }
            if metadata:
                meta.update(metadata)
            
            # Store in vector database
            self.collection.add(
                documents=[text],
                ids=[campaign_id],
                metadatas=[meta]
            )
            return True
        except Exception as e:
            print(f"Error storing campaign in vector memory: {e}")
            return False
    
    def search_similar_campaigns(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar past campaigns using semantic search.
        
        Args:
            query: Search query (e.g., campaign brief or description)
            n_results: Number of results to return
        
        Returns:
            List of similar campaigns with metadata and similarity scores
        """
        if not self.available or not self.collection:
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(n_results, self.collection.count())  # Don't query more than available
            )
            
            similar_campaigns = []
            if results["ids"] and len(results["ids"]) > 0:
                for i in range(len(results["ids"][0])):
                    similar_campaigns.append({
                        "id": results["ids"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if results["distances"] else None,
                        "document": results["documents"][0][i] if results["documents"] else ""
                    })
            
            return similar_campaigns
        except Exception as e:
            print(f"Error searching vector memory: {e}")
            return []
    
    def get_campaign_count(self) -> int:
        """Get the number of campaigns stored in memory."""
        if not self.available or not self.collection:
            return 0
        try:
            return self.collection.count()
        except Exception:
            return 0
    
    def clear_memory(self):
        """Clear all stored campaigns (use with caution)."""
        if not self.available or not self.client:
            return
        
        try:
            # Delete the collection and recreate it
            collection_name = self.collection.name
            self.client.delete_collection(name=collection_name)
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Campaign memory storage for semantic search"}
            )
        except Exception as e:
            print(f"Error clearing vector memory: {e}")





