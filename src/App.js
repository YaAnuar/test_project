import React, { useState, useEffect } from "react";
import io from 'socket.io-client';

import Table from "./TableContainer";
import { SelectColumnFilter } from "./Filter";

import "./App.css";

const socket = io("http://localhost:2000/");

function App() {
  const [data, setData] = useState([]);
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastPong, setLastPong] = useState(null);

  useEffect(() => {
    socket.on('connect', () => {
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
    });

    socket.on('get_data', (res) => {
      console.log('pong')
      setData(res);
    });

    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('pong');
    };
  }, []);

  const sendPing = () => {
    socket.emit('ping');
  }
  // useEffect(() => {
  //   axios("http://localhost/api/table_data")
  //     .then((res) => {
  //       console.log(res.data)
  //       setData(res.data);
  //     })
  //     .catch((err) => console.log(err));
  // }, []);

  const columns = [
    {
      Header: "№ ",
      accessor: "show.num",
    },
    {
      Header: "Заказ №",
      accessor: "show.order",
    },
    {
      Header: "Стоимость,$",
      accessor: "show.USD",
    },
    {
      Header: "Срок поставки",
      accessor: "show.time",
    },
    {
      Header: "Стоимость в руб",
      accessor: "show.RUB",
    },
  ];

  return (
    <div className="App">
      <h1>
        <center>Таблица заказов</center>
      </h1>
      <Table columns={columns} data={data} />
    </div>
  );
}

export default App;
