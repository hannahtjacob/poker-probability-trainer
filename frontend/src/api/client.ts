import axios from 'axios'

import type {
  AiExplanationResult,
  AnalyzeRequest,
  AnalyzeResponse,
  HistoryRecord,
} from '../types/poker'


export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

function getErrorMessage(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return error instanceof Error ? error.message : 'An unexpected error occurred'
  }

  const detail = error.response?.data?.detail

  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => item?.msg)
      .filter((message): message is string => Boolean(message))
      .join(', ')
  }

  if (typeof error.response?.data?.message === 'string') {
    return error.response.data.message
  }

  if (!error.response) {
    return 'Unable to connect to the PokerSense API'
  }

  return error.message || 'The PokerSense API request failed'
}

export async function analyzeHand(
  request: AnalyzeRequest,
): Promise<AnalyzeResponse> {
  try {
    const response = await apiClient.post<AnalyzeResponse>('/analyze', request)
    return response.data
  } catch (error) {
    throw new Error(getErrorMessage(error))
  }
}

export async function getHistory(limit = 20): Promise<HistoryRecord[]> {
  try {
    const response = await apiClient.get<HistoryRecord[]>('/history', {
      params: { limit },
    })
    return response.data
  } catch (error) {
    throw new Error(getErrorMessage(error))
  }
}

export async function explainWithAI(
  analysis: AnalyzeResponse,
): Promise<AiExplanationResult> {
  try {
    const response = await apiClient.post<AiExplanationResult>(
      '/explain',
      analysis,
    )
    return response.data
  } catch (error) {
    throw new Error(getErrorMessage(error))
  }
}
