/**
 * API Client for the AI Todo Chatbot frontend
 */

interface ChatRequest {
  conversation_id?: number;
  message: string;
}

interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<any>;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  /**
   * Send a chat message to the backend
   */
  async sendChatMessage(userId: string, messageData: ChatRequest): Promise<ChatResponse> {
    // Get token from localStorage for authorization
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      body: JSON.stringify(messageData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: ChatResponse = await response.json();
    return data;
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<{ status: string; app: string }> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  }
}

export const apiClient = new ApiClient();

export type { ChatRequest, ChatResponse };