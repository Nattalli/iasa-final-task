FROM node:16

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 8080

RUN npm install -g serve

CMD ["serve", "-s", "dist", "-l", "8080"]
