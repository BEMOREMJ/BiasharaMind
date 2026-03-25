import { BusinessProfileSchema, type BusinessProfile } from "../contracts/business-profile";

export const exampleBusinessProfile: BusinessProfile = BusinessProfileSchema.parse({
  id: "biz_kenya_sunrise_001",
  userId: "user_mark_001",
  businessName: "Sunrise Grocers",
  industry: "retail",
  country: "KE",
  sizeBand: "small",
  yearsOperating: 6,
  revenueBand: "50k_to_250k_usd",
  teamSize: 14,
  mainGoal: "Increase repeat customer sales without adding another branch this year",
  budgetBand: "500_to_2000_usd_per_month",
  currentTools: ["WhatsApp Business", "Google Sheets", "M-Pesa", "Instagram"],
  createdAt: "2026-03-18T18:00:00+00:00",
  updatedAt: "2026-03-18T18:00:00+00:00",
});
