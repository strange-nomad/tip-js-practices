"use strict";

// Класс прикладной ошибки API
export class ApiError extends Error {
  constructor(message, { kind, status = null, code = null, details = null, url = null } = {}) {
    super(message);
    this.name = "ApiError";
    this.kind = kind;
    this.status = status;
    this.code = code;
    this.details = details;
    this.url = url;
  }
}

// Ветка обработки ответа сервера в методе requestJson:
export async function handleResponse(response, url) {
  if (response.ok) {
    return await response.json();
  }

  // При статусах 4xx / 5xx формируется структурированная ошибка:
  let errorPayload = null;
  try {
    errorPayload = JSON.parse(await response.text());
  } catch {}

  const message = errorPayload?.error?.message || `HTTP ошибка ${response.status}`;
  throw new ApiError(message, {
    kind: "http",
    status: response.status,
    code: errorPayload?.error?.code ?? null,
    details: errorPayload?.error?.details ?? null,
    url,
  });
}

// Проверочный вызов getTaskById(999) с перехватом ошибки:
/*
try {
  await api.getTaskById(999);
} catch (error) {
  if (error instanceof ApiError) {
    console.log("Успешный перехват ошибки:");
    console.log("kind:", error.kind);     // "http"
    console.log("status:", error.status); // 404
  } else {
    console.error("Непредвиденная ошибка:", error);
  }
}
*/
