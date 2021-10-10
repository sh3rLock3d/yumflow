import React, { useState } from "react";

import AllProjects from "./AllProjects";
import SelectedProject from "./SelectedProject";

function Flows() {
    const [selectedFlow, setSelectedFlow] = useState(-1) // todo -1
    return (
        <div className="container-fluid">
            <div className="row">
                <AllProjects setSelectedFlow={setSelectedFlow}/>
                <SelectedProject selectedFlow={selectedFlow}/>
            </div>
        </div>
    )
}

export default Flows