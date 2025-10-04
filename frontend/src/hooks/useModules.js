import { useQuery } from "@tanstack/react-query";
import axiosClient from "../api/axiosClient";

const fetch = (path) => () => axiosClient.get(path).then((r) => r.data);

export function useMyProfile() {
  return useQuery(["profile", "me"], fetch("/auth/me/"), {
    staleTime: 1000 * 30,
  });
}

export function useAcademicLeave(params) {
  return useQuery(
    ["academic_leave", params],
    () =>
      axiosClient
        .get("/academic-leave/requests/", { params })
        .then((r) => r.data),
    { staleTime: 1000 * 30 },
  );
}

export function useCalendarEvents() {
  return useQuery(["calendar", "events"], fetch("/calendar/events/"), {
    staleTime: 1000 * 30,
  });
}

export function useDisciplinary() {
  return useQuery(["disciplinary"], fetch("/disciplinary/"), {
    staleTime: 1000 * 30,
  });
}

export function useEmasomo() {
  return useQuery(["emasomo"], fetch("/emasomo/"), { staleTime: 1000 * 60 });
}

export function useExamCards() {
  return useQuery(["exam_card"], fetch("/exam_card/"), {
    staleTime: 1000 * 60,
  });
}

export function useFees() {
  return useQuery(["fees"], fetch("/fees/"), { staleTime: 1000 * 30 });
}

export function useFeedback() {
  return useQuery(["feedback"], fetch("/feedback/"), { staleTime: 1000 * 30 });
}

export function useFinalResults() {
  return useQuery(["final_results"], fetch("/final_results/"), {
    staleTime: 1000 * 60,
  });
}

export function useFinanceRegistration() {
  return useQuery(["finance_registration"], fetch("/finance_registration/"), {
    staleTime: 1000 * 60,
  });
}

export function useGraduation() {
  return useQuery(["graduation"], fetch("/graduation/status/"), {
    staleTime: 1000 * 60,
  });
}

export function useHostel() {
  return useQuery(["hostel"], fetch("/hostel/"), { staleTime: 1000 * 60 });
}

export function useLecturerEvaluation() {
  return useQuery(
    ["lecturer_evaluation"],
    fetch("/lecturer_evaluation/stats/"),
    { staleTime: 1000 * 60 },
  );
}

export function useProvisionalResults() {
  return useQuery(["provisional_results"], fetch("/provisional_results/"), {
    staleTime: 1000 * 60,
  });
}

export function useUnitRegistration() {
  return useQuery(["unit_registration"], fetch("/unit_registration/status/"), {
    staleTime: 1000 * 60,
  });
}

export function useTimetable() {
  return useQuery(["timetable"], fetch("/timetable/"), {
    staleTime: 1000 * 30,
  });
}

export function useAttachments() {
  return useQuery(["attachments"], fetch("/attachments/"), {
    staleTime: 1000 * 30,
  });
}

export function useAccessibility() {
  return useQuery(
    ["accessibility"],
    fetch("/accessibility-ai/accessibility-features/"),
    { staleTime: 1000 * 30 },
  );
}

export function usePayments() {
  return useQuery(["payments"], fetch("/payments/summary/"), {
    staleTime: 1000 * 30,
  });
}
