import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

// Определение схемы базы данных
export default defineSchema({
  // Таблица для хранения сообщений пользователей
  messages: defineTable({
    text: v.optional(v.string(), ""),
    timestamp: v.optional(v.number(), 0),
    userId: v.optional(v.string(), ""),
    username: v.optional(v.string(), ""),
    phone_number: v.optional(v.string(), ""),
    intent: v.optional(v.string(), ""),
    full_name: v.optional(v.string(), ""),
    fullname: v.optional(v.string(), ""),
  }),
}); 