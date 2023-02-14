FROM node:18.14.0

WORKDIR /

COPY . .

RUN npm install

EXPOSE 80

CMD ["npm", "run", "dev",  "--", "--host", "0.0.0.0", "--port", "80"]