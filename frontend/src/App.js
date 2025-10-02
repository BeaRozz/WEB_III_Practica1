// App.js
import React, { useState, useEffect, useCallback } from "react";
import Swal from 'sweetalert2';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './App.css'; 

const successEmbeds = [
  { embedHtml: `<iframe width="450" height="315" 
                  src="https://www.youtube.com/embed/_e9yMqmXWo0?si=KumTQ5DwjrZeBG_p&controls=0&autoplay=1" 
                  title="YouTube video player" 
                  frameborder="0" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                  referrerpolicy="strict-origin-when-cross-origin" 
                  allowfullscreen>
                </iframe>` },
  { embedHtml: `<iframe width="450" height="315" 
                  src="https://www.youtube.com/embed/ATulXvTNG6Y?si=CGZYR1FXIZc7a2bu&controls=0&autoplay=1" 
                  title="YouTube video player" 
                  frameborder="0" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                  referrerpolicy="strict-origin-when-cross-origin" 
                  allowfullscreen>
                </iframe>` },
  { embedHtml: `<iframe width="450" height="315" 
                src="https://www.youtube.com/embed/u4ecB57jFhI?si=EoQDOHq9VvMJ72rE&controls=0&autoplay=1" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
              </iframe>` },
  { embedHtml: `<iframe width="450" height="315" 
                src="https://www.youtube.com/embed/3xotxtnAxiM?autoplay=1&controls=0" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
              </iframe>` },
  { embedHtml: `<iframe width="450" height="315" 
                src="https://www.youtube.com/embed/NOvglrc_-PE?autoplay=1&controls=0" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
              </iframe>` }
              
];

const errorEmbeds = [
  { embedHtml: `<iframe 
                width="450" 
                height="315" 
                src="https://www.youtube.com/embed/mQ-9NPtsh0c?si=AkjGl8pER1M5qu3y&autoplay=1&controls=0" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
              </iframe>` },
  { embedHtml: `<iframe width="450" height="315" 
                src="https://www.youtube.com/embed/xVWeRnStdSA?si=bOCliJcx3xRX7-0d&controls=0&autoplay=1" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
              </iframe>` },
  { embedHtml: `<iframe width="450" height="315" 
                src="https://www.youtube.com/embed/xsvZOUnXdWM?si=NMFH8ladoefmtWgy&controls=0&autoplay=1" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
              </iframe>` },
  { embedHtml: `<iframe width="450" height="315" 
  src="https://www.youtube.com/embed/adaanODbWy4?si=P2XSQqE7vMn9ZfGf&controls=0&start=14&autoplay=1" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
              </iframe>` },
  { embedHtml: `<iframe width="450" height="315" 
                src="https://www.youtube.com/embed/AxaI0lrjwMk?si=CIxz5VqPtNxjz_39&controls=0&start=41&autoplay=1" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
              </iframe>` }
];

const showAlert = (isSuccess, message) => {
  const chosenList = isSuccess ? successEmbeds : errorEmbeds;
  const randomIndex = Math.floor(Math.random() * chosenList.length);
  const chosenItem = chosenList[randomIndex];

  Swal.fire({
    title: isSuccess ? '¡Éxito!' : '¡Oops!',
    html: `
      <div style="width: 100%; aspect-ratio: 16 / 9;">
        ${chosenItem.embedHtml}
      </div>
      <p style="margin-top: 1em;">${message}</p> 
    `,
    showConfirmButton: true,
    confirmButtonText: 'Entendido',
    confirmButtonColor: '#ff85a1'
  });
};




// --- Componente Calculadora ---
function Calculator({ onCalculationSuccess }) {
  const [numbers, setNumbers] = useState(["", ""]);
  const [operation, setOperation] = useState("sum");
  const [resultado, setResultado] = useState(null);

  const handleNumberChange = (index, value) => {
    if (!/^\d*\.?\d*$/.test(value)) return;
    if (resultado !== null) {
      setResultado(null);
    }
    const newNumbers = [...numbers];
    newNumbers[index] = value;
    if (index === numbers.length - 1 && value !== "") {
      newNumbers.push("");
    }
    setNumbers(newNumbers);
  };

  const handleKeyDown = (e) => {
    if (!/[0-9]/.test(e.key) && !['Backspace', 'ArrowLeft', 'ArrowRight', 'Tab', 'Enter', '.'].includes(e.key)) {
      e.preventDefault();
    }
    if (e.key === 'Enter') {
      e.preventDefault();
      handleCalculate();
    }
  };


  const handleCalculate = async () => {
    const validNumbers = numbers.map(n => parseFloat(n)).filter(n => !isNaN(n));
    if (validNumbers.length < 2) {
      showAlert(false, 'Necesitas al menos dos números para realizar una operación.');
      return;
    }
    try {
      const res = await fetch(`http://localhost:8089/calculadora/${operation}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nums: validNumbers })
      });
      const data = await res.json();
      if (!res.ok) {
        throw data;
      }

      if (operation === 'div' && (data.resultado === null || !isFinite(data.resultado))) {
        showAlert(false, 'Error: No se puede dividir por cero.');
        return;
      }


      setResultado(data.resultado);
      showAlert(true, `El resultado de la operación es: ${data.resultado}`);
      onCalculationSuccess();
      setNumbers(["", ""]);
    } catch (errorData) {
      let errorMessage = 'Ocurrió un error inesperado.';
      
      // Verificamos si existe el campo "error" y si es un array con contenido
      if (errorData && Array.isArray(errorData.error) && errorData.error.length > 0) {
        // Tomamos solo el primer mensaje de la lista
        errorMessage = errorData.error[0];
      } 
      
      showAlert(false, errorMessage);
    }
  };
  
  return (
    <div className="panel calculator">
      <h2>Calculadora:</h2>
      <label htmlFor="op-select">Elija el tipo de operación:</label>
      <select id="op-select" value={operation} onChange={(e) => setOperation(e.target.value)}>
        <option value="sum">Suma</option>
        <option value="res">Resta</option>
        <option value="mul">Multiplicación</option>
        <option value="div">División</option>
      </select>

      <div className="numbers-container">
        {numbers.map((num, index) => (
          <React.Fragment key={index}>
            <input
              type="text"
              value={num}
              onChange={(e) => handleNumberChange(index, e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="..."
              className={`number-box ${num ? 'has-value' : ''}`}
            />
            {index < numbers.filter(n => n !== "").length - 1 && <span className="operator-symbol">{ {sum:'+', res:'-', mul:'×', div:'÷'}[operation] }</span>}
          </React.Fragment>
        ))}
      </div>
      
      {/* Se envuelve el botón y el resultado en un div para alinearlos */}
      <div className="result-container">
          <button onClick={handleCalculate} className="result-button">Obtener resultado</button>
          {resultado !== null && <span className="result-display">= {resultado}</span>}
      </div>
    </div>
  );
}




// --- Componente Historial ---
function History({ refreshTrigger }) {
  const [historial, setHistorial] = useState([]);
  const [loading, setLoading] = useState(true);
  const [opFilter, setOpFilter] = useState("");
  const [order, setOrder] = useState("desc");
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const fetchHistorial = useCallback(async () => {
    setLoading(true);
    let url = "http://localhost:8089/historial?";
    const params = new URLSearchParams();
    if(opFilter) params.append('operacion', opFilter);
    if(order) params.append('orden', order);
    if(startDate) params.append('fecha_inicio', startDate.toISOString().split('T')[0]);
    if(endDate) params.append('fecha_fin', endDate.toISOString().split('T')[0]);
    url += params.toString();

    try {
      const res = await fetch(url);
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'No se pudo cargar el historial.');
      }
      const data = await res.json();
      setHistorial(data.historial);
    } catch (error) {
      showAlert(false, error.message);
      setHistorial([]);
    } finally {
      setLoading(false);
    }
  }, [opFilter, order, startDate, endDate]);

  useEffect(() => {
    fetchHistorial();
  }, [refreshTrigger, fetchHistorial]);

  return (
    <div className="panel history">
      <h2>Historial:</h2>
      <div className="filters">
        <select value={opFilter} onChange={(e) => setOpFilter(e.target.value)}>
          <option value="">Todas</option>
          <option value="sum">Suma</option>
          <option value="res">Resta</option>
          <option value="mul">Multiplicación</option>
          <option value="div">División</option>
        </select>
        <select value={order} onChange={(e) => setOrder(e.target.value)}>
          <option value="desc">Desc</option>
          <option value="asc">Asc</option>
        </select>
        <DatePicker
          selected={startDate}
          onChange={(date) => setStartDate(date)}
          selectsStart
          startDate={startDate}
          endDate={endDate}
          maxDate={endDate}
          isClearable
          placeholderText="Inicio"
          className="date-picker"
        />
        <DatePicker
          selected={endDate}
          onChange={(date) => setEndDate(date)}
          selectsEnd
          startDate={startDate}
          endDate={endDate}
          minDate={startDate}
          isClearable
          placeholderText="Fin"
          className="date-picker"
        />
      </div>
      <ul className="history-list">
        {loading ? (
          <li>Cargando...</li>
        ) : historial.length > 0 ? (
          historial.map((op, i) => (
            <li key={i}>
              <div className="history-item-line history-op-result">
                <span>Operación: {op.operacion}</span>
                <span>Resultado: {op.resultado}</span>
              </div>
              <div className="history-item-line">
                Números: <span>{Array.isArray(op.nums) ? op.nums.join(', ') : 'N/A'}</span>
              </div>
              <div className="history-date">
                {new Date(op.date).toLocaleString()}
              </div>
            </li>
          ))
        ) : (
          <li className="no-history">No hay historial disponible</li>
        )}
      </ul>
    </div>
  );
}

// --- Componente Principal ---
function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const handleSuccess = () => {
    setRefreshKey(prevKey => prevKey + 1);
  };
  return (
    <div className="App">
      <header>
        <h1>Welcome to mi Calculadora</h1>
      </header>
      <main>
        <Calculator onCalculationSuccess={handleSuccess} />
        <History refreshTrigger={refreshKey} />
      </main>
    </div>
  );
}

export default App;