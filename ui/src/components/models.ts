import { IncidentReportDto } from "./ChatMessage";

export type Message = {
  role: string;
  content: string;
  follow_up_questions?: string[];
  incident_report?: IncidentReport;
  incident_reports?: IncidentReportDto[];
};

export interface IncidentReport {
  desc: string;
  explanation: string;
  action: string;
  reported_by?: string; // use string for UUID
}

export interface MessageProps {
  role: "user" | "bot";
  content: string;
  follow_up_questions?: string[];
  incident_report?: {
    desc: string;
    explanation: string;
    action: string;
    reported_by?: string;
  };
}
