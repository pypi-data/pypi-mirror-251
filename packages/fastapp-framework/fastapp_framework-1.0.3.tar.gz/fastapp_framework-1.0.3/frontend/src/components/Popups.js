import { FaCircleXmark } from "react-icons/fa6";

import { Column, Columns } from "./Columns";

const Popup = (props) => {
    return (
        <div className={props.popupClass} hidden={!props.active}>
            <Columns>
                <Column args={"is-1"}>
                    <a href="/closebox" onClick={(e) => {
                        e.preventDefault();
                        props.setActive(false);
                    }}>
                        <span className="has-text-light">
                            <FaCircleXmark />
                        </span>
                    </a>
                </Column>
                <Column args={"is-offset-2"}>
                    <p className="subtitle">{props.message}</p>
                </Column>
            </Columns>
        </div>
    )
}

export default Popup;