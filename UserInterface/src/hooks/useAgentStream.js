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

    const [searchQueries, setSearchQueries] = useState([]);
    const [foundUrls, setFoundUrls] = useState([]); // The list of 15+ sources found
    const [currentAction, setCurrentAction] = useState(""); // "Reading: cnn.com..."


    //event connection 
    const startStream = (topic) => {
        if (!topic.trim()) return;

        setStatus("processing");
        setLogs([]);
        setReport("");
        setSources([]);
        setSearchQueries([]);
        setFoundUrls([]);
        setCurrentAction("Initializing Agent...");

        const eventSource = new EventSource(`http://localhost:8000/stream?topic=${encodeURIComponent(topic)}`);

        eventSource.onmessage = (event) => {
            try{
                const parsedData = JSON.parse(event.data);
    
                if(parsedData.type === 'log'){
                    if (parsedData.step === 'planner') {
                        setSearchQueries(parsedData.details);
                        setCurrentAction("Generating Search Queries...");
                    } 
                    else if (parsedData.step === 'sources') {
                        setFoundUrls(parsedData.details);
                        setCurrentAction("Reviewing Sources...");
                    }
                    else if (parsedData.step === 'scraping') {
                        setCurrentAction(`Reading: ${new URL(parsedData.details).hostname}...`);
                    }
                
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
        report,
        sources,
        searchQueries,     
        foundUrls,       
        currentAction,         
        startStream,
        resetStream
    };

};