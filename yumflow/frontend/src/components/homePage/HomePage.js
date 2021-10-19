import React, {useEffect, useContext} from 'react';

import {Context} from '../../Store'

function Homepage() {
    
    const [state, dispatch] = useContext(Context);
    console.log(state)

    return (
        <div className="container-fluid">
            <p>hihiihihh</p>
        </div>
    )
}

export default Homepage;