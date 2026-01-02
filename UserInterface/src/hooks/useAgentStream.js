import { useState } from "react";

export const useAgentStream = () => {
    //different processing status like idle/ processing/ finished
    const [status, setStatus] = useState("idle");

    //this will hold the logs sent from our agent
    const [logs, setLogs] = useState([]);

    //this will hold the report created by agent
    const [report, setReport] = useState("");

    //hold all the sources of the report for the references
    const [sources, setSources] = useState([]);

    //event connection 
    const startStream = (topic) => {
        if (!topic.trim()) return;

        setStatus("processing");
        setLogs([]);
        setReport("");
        setSources([]);

        const eventSource = new EventSource(`http://localhost:8000/stream?topic=${encodeURIComponent(topic)}`);

        eventSource.onmessage = (event) => {
            try{
                const parsedData = JSON.parse(event.data);
    
                if(parsedData.type === 'log'){
                    setLogs(prev => [...prev, parsedData.message]);
                }else if(parsedData.type === 'result'){
                    setReport(parsedData.markdown);
                    setSources(parsedData.sources);
                    setStatus("finished");
                    eventSource.close();
                }
            }
            catch(exec){
                console.log(exec);
            }
        };

        eventSource.onerror = () => {
            console.error("Stream connection lost");
            // Checking the state of the connection
            if (eventSource.readyState === EventSource.CLOSED) {
                console.log("Connection was closed by the server.");
            } else if (eventSource.readyState === EventSource.CONNECTING) {
                console.log("Connection lost. Attempting to reconnect...");
            }
            eventSource.close();
            setStatus("idle");
        }
    };

    // reset conneciton
    const resetStream = () => {
        setStatus("idle");
        
    };

    return {
        status,
        logs,
        report,
        sources,
        startStream,
        resetStream
    };

};