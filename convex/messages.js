// Файл функций Convex для сохранения сообщений пользователей
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

// Функция сохранения сообщения в базу данных
export const save = mutation({
  args: {
    text: v.optional(v.string(), ""),
    timestamp: v.optional(v.number(), 0),
    userId: v.optional(v.string(), ""),
    username: v.optional(v.string(), ""),
    phone_number: v.optional(v.string(), ""),
    intent: v.optional(v.string(), ""),
    full_name: v.optional(v.string(), ""),
    fullname: v.optional(v.string(), ""),
  },
  handler: async (ctx, args) => {
    const messageId = await ctx.db.insert("messages", args);
    return messageId;
  },
});

// Функция для получения списка всех сообщений
export const list = query({
  args: {},
  handler: async (ctx) => {
    const messages = await ctx.db.query("messages").collect();
    return messages;
  },
}); 