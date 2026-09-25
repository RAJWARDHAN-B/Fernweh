import { expect, test } from "@playwright/test";

test("home page renders with security headers", async ({ page }) => {
  const response = await page.goto("/");

  await expect(page.getByRole("heading", { level: 1, name: "Fernweh" })).toBeVisible();
  expect(response?.headers()["x-frame-options"]).toBe("DENY");
  expect(response?.headers()["x-powered-by"]).toBeUndefined();
});
