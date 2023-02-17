FROM node:18.14.0

WORKDIR /app

COPY package.json .

RUN npm i

COPY . .

EXPOSE 5050

CMD ["npm", "run", "dev"]