FROM node:21-alpine AS builder
WORKDIR /app

ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_NAME

ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV NEXT_PUBLIC_NAME=${NEXT_PUBLIC_NAME}

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

FROM node:21-alpine AS runner
WORKDIR /app

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.mjs ./

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

RUN chown -R nextjs:nodejs /app/.next /app/public

USER nextjs

ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_NAME

ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV NEXT_PUBLIC_NAME=${NEXT_PUBLIC_NAME}

EXPOSE ${FRONTEND_PORT}

CMD sh -c "npx next start -H 0.0.0.0 -p ${FRONTEND_PORT}"