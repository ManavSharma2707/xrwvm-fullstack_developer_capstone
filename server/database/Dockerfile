FROM node:20-bookworm-slim

WORKDIR /app

# Install dependencies first so they are cached between builds
COPY package.json ./
RUN npm install --omit=dev

# App code, plus the seed data next to app.js
COPY app.js review.js dealership.js inventory.js ./
COPY data/dealerships.json data/reviews.json ./

EXPOSE 3030

CMD [ "node", "app.js" ]
