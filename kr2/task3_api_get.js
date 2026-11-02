"use strict";

// Фабрика методов работы с API задач (ПР5)
export function createTaskApi(client) {
  async function getTasks(filters = {}) {
    const query = {};
    if ("completed" in filters) query.completed = filters.completed;
    if ("priority" in filters) query.priority = filters.priority;
    if ("categoryId" in filters) query.categoryId = filters.categoryId;
    if ("q" in filters) query.q = filters.q;

    // Выполнение HTTP GET-запроса с query-параметрами: /tasks?completed=false&priority=high
    const result = await client.requestJson("/tasks", { query });
    return {
      tasks: result.data,
      meta: result.meta,
    };
  }

  return { getTasks };
}

// Демонстрационный вызов (результаты при обращении к серверу ПР5):
/*
const client = createApiClient({ baseUrl: "http://localhost:3000/api" });
const api = createTaskApi(client);

const { tasks, meta } = await api.getTasks({ completed: false, priority: "high" });
console.log("Идентификаторы невыполненных задач с высоким приоритетом:", tasks.map(t => t.id)); // [4, 13, 34]
console.log("Всего найдено (meta.total):", meta.total); // 3
*/
