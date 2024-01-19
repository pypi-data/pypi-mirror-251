import Navbar from "./navbar/Navbar"
import Footer from "./Footer"

export default function Outline(props){

    return (
        <div className="hero is-dark is-fullheight">
            <Navbar />
            {props.children}
            <Footer />
        </div>
    )
}