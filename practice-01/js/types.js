"use strict";

console.log("=== Задание 2. Исследование типов и преобразований ===");

const expressions = [
  { expr: '"8" + 2', val: "8" + 2 },
  { expr: '"8" - 2', val: "8" - 2 },
  { expr: 'Number("8") + 2', val: Number("8") + 2 },
  { expr: '"12" > "3"', val: "12" > "3" },
  { expr: '12 === "12"', val: 12 === "12" },
  { expr: 'Number("")', val: Number("") },
  { expr: 'Number("text")', val: Number("text") },
  { expr: 'Boolean("false")', val: Boolean("false") },
  { expr: 'typeof null', val: typeof null },
  { expr: 'typeof NaN', val: typeof NaN },
];

for (let i = 0; i < expressions.length; i++) {
  const item = expressions[i];
  console.log(`${i + 1}. Выражение: ${item.expr}`);
  console.log(`   Результат: ${item.val}`);
  console.log(`   Тип результата: ${typeof item.val}`);
}
