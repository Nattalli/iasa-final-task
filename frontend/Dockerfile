FROM node:16

WORKDIR /frontend

RUN npm install -g vite

COPY . /frontend
RUN npm install
EXPOSE 5173

CMD ["npm", "run", "serve"]
