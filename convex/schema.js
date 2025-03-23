import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

// Определение схемы базы данных
export default defineSchema({
  // Таблица для хранения сообщений пользователей
  messages: defineTable({
    // Основные поля
    userId: v.string(),
    recipientId: v.string(),
    content: v.string(),
    source: v.string(),
    status: v.string(),
    createdAt: v.number(),
    
    // Опциональные поля
    errorMessage: v.optional(v.string()),
    username: v.optional(v.string()),
    phone_number: v.optional(v.string()),
    intent: v.optional(v.string()),
    full_name: v.optional(v.string())
  }),
}); 