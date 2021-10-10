import React, { useState } from "react";

function Header() {
    return (
        <nav className="navbar navbar-expand-lg bg-primary text-white">
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarTogglerDemo01">
                <h3> یادگیری چرخه ی ماشین </h3>

            </div>
        </nav>
    )
}

export default Header