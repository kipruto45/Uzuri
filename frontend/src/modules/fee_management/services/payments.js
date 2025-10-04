import api from "../../api/client";

const prefix = "/api/v1/payments";

export function listPayments(params) {
  return api.get(prefix + "/", { params });
}

export function mpesaCheckout(payload) {
  return api.post(prefix + "/mpesa/", payload);
}

export function stripeCheckout(payload) {
  return api.post(prefix + "/stripe/", payload);
}

export default { listPayments, mpesaCheckout, stripeCheckout };
