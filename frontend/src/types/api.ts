// All TypeScript types live here — import them anywhere in the project

export interface SlideRequest {
  prompt: string; // the topic the user typed
  slide_count: number; // how many slides to generate
  theme?: string; // optional — ? means it can be omitted
}

export interface ApiError {
  message: string;
  status: number;
}
