FROM node:18.14.0

WORKDIR /app

COPY package.json .

RUN npm i

COPY . .

EXPOSE 6060

CMD ["npm", "run", "dev"]