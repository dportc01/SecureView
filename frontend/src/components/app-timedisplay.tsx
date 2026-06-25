import { useEffect, useState } from "react";

export function TimeDisplay() {
  const [time, setTime] = useState<string>(new Date().toLocaleString());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date().toLocaleString());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <section>
      <h2 className="text-base">Hora actual: {time}</h2>
    </section>
  );
}
