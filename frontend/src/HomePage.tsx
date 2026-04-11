import { useEffect, useState } from "react";
import "./index.css";

function HomePage() {
  return (
    <div>
      <Banner />
      <div className="flex flex-row">
        <Sidebar />
        <Content />
      </div>
    </div>
  );
}

function Banner() {
  return (
    <div className="border-8 border-gray-300 flex justify-center text-4xl tracking-[0.7em] font-bold uppercase py-4">
      <h1>Secure View</h1>
    </div>
  );
}

function Sidebar() {
  return (
    <div className="bg-gray-300 w-fit px-4">
      <h3 className="my-4 text-[18px]">Página principal</h3>
      <h3 className="my-4 text-[18px]">Cámaras</h3>
      <h3 className="my-4 text-[18px]">Almacenamiento</h3>
      <h3 className="my-4 text-[18px]">Notificariones</h3>
      <h3 className="my-4 text-[18px]">Ajustes</h3>
    </div>
  );
}

function Content() {
  return (
    <div className="flex flex-col flex-1 ml-8 mt-4 space-y-4">
      <TimeDisplay />
      <Notifications />
      <Video />
    </div>
  );
}

function TimeDisplay() {
  const [time, setTime] = useState<string>(new Date().toLocaleString());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date().toLocaleString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2 className="text-2xl">Hora actual: {time}</h2>
    </div>
  );
}

function Notifications() {
  return (
    <div>
      <h2 className="text-2xl">Últimas notificaciones</h2>
    </div>
  );
}

function Video() {
  return (
    <div>
      <h2 className="text-2xl mb-2">Cámaras principales</h2>

      <img
        src="http://localhost:5000/video"
        alt="Camera Stream"
        className="w-[640px] rounded-lg"
      />
    </div>
  );
}

export default HomePage;