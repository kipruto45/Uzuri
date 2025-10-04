export function formatCurrency(amount, locale = "en-KE", currency = "KES") {
  if (amount == null) return "";
  return new Intl.NumberFormat(locale, { style: "currency", currency }).format(
    amount,
  );
}
