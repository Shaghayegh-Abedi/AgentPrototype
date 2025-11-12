"""
Agent communication protocol for inter-agent messaging.
Enables agents to request information, share data, and coordinate dynamically.
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


class MessageType(Enum):
    """Types of messages agents can send."""
    REQUEST = "request"  # Request information or action
    RESPONSE = "response"  # Response to a request
    NOTIFICATION = "notification"  # Informational message
    QUERY = "query"  # Query for data
    PROPOSAL = "proposal"  # Propose a solution or approach


@dataclass
class AgentMessage:
    """Structured message for agent-to-agent communication."""
    from_agent: str
    to_agent: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    requires_response: bool = False
    message_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    correlation_id: Optional[str] = None  # Links request-response pairs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        return {
            "message_id": self.message_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "message_type": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "requires_response": self.requires_response,
            "correlation_id": self.correlation_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create message from dictionary."""
        return cls(
            message_id=data.get("message_id", str(datetime.now().timestamp())),
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            message_type=MessageType(data["message_type"]),
            content=data["content"],
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            requires_response=data.get("requires_response", False),
            correlation_id=data.get("correlation_id")
        )


class AgentCommunicationBus:
    """Message bus for agent communication."""
    
    def __init__(self):
        """Initialize the communication bus."""
        self.messages: List[AgentMessage] = []
        self.pending_requests: Dict[str, AgentMessage] = {}  # correlation_id -> request
    
    def send_message(self, message: AgentMessage):
        """
        Send a message between agents.
        
        Args:
            message: The message to send
        """
        self.messages.append(message)
        
        # Track pending requests
        if message.requires_response and message.message_type == MessageType.REQUEST:
            self.pending_requests[message.message_id] = message
        
        # Remove from pending when responded to
        if message.message_type == MessageType.RESPONSE and message.correlation_id:
            self.pending_requests.pop(message.correlation_id, None)
    
    def get_messages_for_agent(self, agent_name: str, message_type: Optional[MessageType] = None) -> List[AgentMessage]:
        """
        Get messages for a specific agent.
        
        Args:
            agent_name: Name of the agent
            message_type: Optional filter by message type
        
        Returns:
            List of messages for the agent
        """
        messages = [msg for msg in self.messages if msg.to_agent == agent_name]
        if message_type:
            messages = [msg for msg in messages if msg.message_type == message_type]
        return messages
    
    def get_pending_requests_for_agent(self, agent_name: str) -> List[AgentMessage]:
        """
        Get pending requests for a specific agent.
        
        Args:
            agent_name: Name of the agent
        
        Returns:
            List of pending requests
        """
        return [
            msg for msg in self.pending_requests.values()
            if msg.to_agent == agent_name
        ]
    
    def get_conversation_history(self, agent1: str, agent2: str) -> List[AgentMessage]:
        """
        Get conversation history between two agents.
        
        Args:
            agent1: First agent name
            agent2: Second agent name
        
        Returns:
            List of messages between the two agents
        """
        return [
            msg for msg in self.messages
            if (msg.from_agent == agent1 and msg.to_agent == agent2) or
               (msg.from_agent == agent2 and msg.to_agent == agent1)
        ]
    
    def create_response(self, original_message: AgentMessage, response_content: Dict[str, Any]) -> AgentMessage:
        """
        Create a response message to an original message.
        
        Args:
            original_message: The original message to respond to
            response_content: The response content
        
        Returns:
            Response message
        """
        return AgentMessage(
            from_agent=original_message.to_agent,
            to_agent=original_message.from_agent,
            message_type=MessageType.RESPONSE,
            content=response_content,
            correlation_id=original_message.message_id,
            requires_response=False
        )
    
    def get_message_statistics(self) -> Dict[str, Any]:
        """Get statistics about messages in the bus."""
        stats = {
            "total_messages": len(self.messages),
            "pending_requests": len(self.pending_requests),
            "messages_by_type": {},
            "messages_by_agent": {}
        }
        
        for msg in self.messages:
            # Count by type
            msg_type = msg.message_type.value
            stats["messages_by_type"][msg_type] = stats["messages_by_type"].get(msg_type, 0) + 1
            
            # Count by agent
            stats["messages_by_agent"][msg.from_agent] = stats["messages_by_agent"].get(msg.from_agent, 0) + 1
        
        return stats
    
    def clear_messages(self):
        """Clear all messages (use with caution)."""
        self.messages = []
        self.pending_requests = {}





