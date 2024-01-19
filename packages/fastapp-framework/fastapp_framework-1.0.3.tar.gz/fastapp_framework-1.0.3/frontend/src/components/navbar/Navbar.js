import { useCookies } from "react-cookie";

export default function Navbar(props){
    const [cookies, , removeCookies] = useCookies(['fastapp_token']);

    const isLoggedIn = cookies.fastapp_token !== undefined;
    const isAdmin = (cookies.fastapp_token !== undefined) ? 
        (cookies.fastapp_token.grants.find((value) => value === "admin") !== undefined) : false;

    return (
        <div className="navbar">
            <div className="navbar-brand">
                <a className="navbar-item" href="/">
                    <img src="/fastapp-logo.png" width="112" height="28" alt="Fastapp Logo"></img>
                </a>

                <a href="/open-nav" role="button" className="navbar-burger" aria-label="menu"
                   aria-expanded="false" data-target="navbarBasicExample" onClick={(e) => {
                        e.preventDefault();
                        document.getElementById("navbarBasicExample").classList.toggle("is-active");
                   }}>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </a>
            </div>

            <div className="navbar-menu" id="navbarBasicExample">
                <div className="navbar-start">
                    <div className="navbar-item">
                        <a className="subtitle" href="/about">About</a>
                    </div>
                </div>
                <div className="navbar-end">
                    {isAdmin && <div className="navbar-item">
                        <a className="subtitle" href="/admin">Admin</a>
                    </div>}
                    {!isLoggedIn && <div className="navbar-item">
                        <a className="button" href="/login">Login</a>
                    </div>}
                    {isLoggedIn && <div className="navbar-item">
                        <a className="button is-danger" href="/logout" onClick={(e) => {
                            e.preventDefault();
                            window.location.replace("/login")
                            removeCookies("fastapp_token")
                        }}>Logout</a>
                    </div>}
                </div>
            </div>
        </div>
    )
}

