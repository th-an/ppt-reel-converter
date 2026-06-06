export interface SlideFingerprint {
  slide_number: number;
  title_text: string | null;
  body_texts: string[];
  bullet_items: string[];
  image_count: number;
  image_names: string[];
  total_word_count: number;
  unique_numbers: string[];
  content_type: string;
  element_count: number;
  primary_color: string | null;
  fonts_used: string[];
  has_smart_art: boolean;
  has_chart: boolean;
  warnings: string[];
}

export interface Scene {
  layout: string;
  headline: string | null;
  body_items: string[];
  stat_number: string | null;
  stat_label: string | null;
  stat_sublabel: string | null;
  image_name: string | null;
  image_crop: string;
  image_caption: string | null;
  quote_text: string | null;
  quote_attribution: string | null;
  cta_headline: string | null;
  cta_subheadline: string | null;
}

export interface CoverageDeclaration {
  title_preserved: boolean;
  title_text: string | null;
  all_bullets_addressed: boolean;
  all_images_addressed: boolean;
  all_numbers_preserved: boolean;
  numbers_list: string[];
  total_scenes: number;
  estimated_total_words: number;
}

export interface VerificationResult {
  slide_number: number;
  title_match: boolean;
  all_bullets_present: boolean;
  all_numbers_present: boolean;
  all_images_present: boolean;
  missing_words: string[];
  missing_numbers: string[];
  missing_images: string[];
  score: number;
  passed: boolean;
  flags: string[];
}

export interface RenderedScene {
  scene_number: number;
  layout_used: string;
  placeholders_filled: Record<string, string>;
  images_inserted: string[];
  has_text_overflow: boolean;
  min_font_size_pt: number | null;
}

export type ApprovalAction = "approve" | "retry" | "change_layout" | "edit_content" | "skip";

export type AppPhase =
  | "upload"
  | "scanning"
  | "template_select"
  | "processing"
  | "awaiting_approval"
  | "reprocessing"
  | "editing"
  | "complete"
  | "exporting";

export interface AppState {
  phase: AppPhase;
  fingerprints: SlideFingerprint[];
  currentSlideIndex: number;
  totalSlides: number;
  currentResult: ProcessSlideResponse | null;
  approvedSlides: Set<number>;
  skippedSlides: Set<number>;
  selectedTemplate: string;
  error: string | null;
}

export interface ProcessSlideResponse {
  slide_number: number;
  gate2: {
    status: "PASS" | "FAIL";
    coverage: CoverageDeclaration;
    scenes: Scene[];
  };
  gate3: {
    status: "PASS" | "FAIL" | "RETRY";
    details: {
      empty_scenes: number[];
      text_overflow_count: number;
      font_size_ok: boolean;
    };
  };
  gate4: {
    status: "PASS" | "FAIL" | "FLAG";
    score: number;
    details: VerificationResult;
  };
  scenes: RenderedScene[];
  preview_images: string[];
}

export interface FinalReport {
  input_file: string;
  output_file: string | null;
  template_used: string;
  total_slides_input: number;
  total_scenes_output: number;
  slides_approved: number;
  slides_skipped: number;
  slides_flagged: number;
  average_score: number;
  per_slide_scores: Record<number, number>;
}

export interface TemplateConfig {
  template_name: string;
  safe_zone: { top_pct: number; bottom_pct: number };
  brand: { primary_color: string; header_font: string; body_font: string };
  layout_mappings: Record<string, { layout_index: number; layout_name: string }>;
  content_type_routing: Record<string, string>;
  fallback_layout_name: string;
}

declare global {
  interface Window {
    electronAPI: {
      selectFile: () => Promise<string | null>;
      selectOutputDir: () => Promise<string | null>;
      startPythonSidecar: (args: {
        filePath: string;
        templateStyle: string;
        apiKey?: string;
        useAi?: boolean;
      }) => Promise<{ success: boolean; output: string }>;
    };
  }
}
