"use strict";

// Фрагменты изменения статуса задачи и перезагрузки списка в ПР6

// 1. Контроллер: метод toggleTask с оптимистичной/асинхронной мутацией
async function toggleTask(id) {
  const target = tasks.find((t) => t.id === id);
  if (!target) return;

  await performMutation(async () => {
    // Отправка PATCH-запроса на изменение статуса задачи
    await api.setTaskCompleted(id, !target.completed);
    view.notify("Статус задачи обновлен.", "success");
  });
}

// 2. Обертка мутации данных с последующим повторным запросом актуального списка
async function performMutation(action) {
  view.setMutationPending(true);
  try {
    await action();
    // Повторная загрузка списка с сохранением активного фильтра (completed=false)
    await loadData(false);
  } catch (error) {
    view.notify(messageForError(error), "error");
  } finally {
    view.setMutationPending(false);
  }
}

// 3. Метод клиента taskApi для отправки PATCH /api/tasks/:id
async function setTaskCompleted(id, completed, options = {}) {
  const response = await client.requestJson(`/tasks/${id}`, {
    method: "PATCH",
    body: { completed },
    signal: options?.signal,
  });
  return response.data;
}
