import { mutation } from "./_generated/server";

// Функция сохранения сообщения
export const save = mutation(async ({ db }, args) => {
  const {
    userId,
    recipientId,
    content,
    source,
    status,
    createdAt,
    errorMessage,
    username,
    phone_number,
    intent,
    full_name
  } = args;

  // Сохраняем сообщение в базу данных
  const message = await db.insert("messages", {
    userId,
    recipientId,
    content,
    source,
    status,
    createdAt,
    ...(errorMessage && { errorMessage }),
    ...(username && { username }),
    ...(phone_number && { phone_number }),
    ...(intent && { intent }),
    ...(full_name && { full_name })
  });

  return message;
}); 