import { useState } from "react"


const MenuLink = (props) => {
    const [hovered, setHovered] = useState(false);
    
    const activeClass = (props.active === props.children) ? 'is-active': '';
    const hoverClass = hovered ? 'has-text-dark' : ''

    return (
        <a className={`${props.classArgs} ${activeClass} ${hoverClass}`} href={`/${props.children}`} onClick={(e) => {
            e.preventDefault();
            props.setActive(props.children)
        }} onMouseEnter={() => setHovered(true)} onMouseLeave={() => setHovered(false)}>
            {props.children}
        </a>
    )
}

const AdminMenu = (props) => {

    return (
        <div>
            <aside className="menu is-hidden-mobile">
                <p className="menu-label">
                    General
                </p>
                <ul className="menu-list">
                    <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Dashboard</MenuLink></li>
                    <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Something</MenuLink></li>
                </ul>
                <p className="menu-label">
                    Administration
                </p>
                <ul className="menu-list">
                    <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>User Settings</MenuLink></li>
                    <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Administration</MenuLink></li>
                    <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Manage Users</MenuLink>
                    <ul>
                        <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Members</MenuLink></li>
                        <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Admins</MenuLink></li>
                        <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Add Users</MenuLink></li>
                    </ul>
                    </li>
                    <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Permissions</MenuLink></li>
                    <li><MenuLink setActive={props.setActive} active={props.active} classArgs={''}>Authentication</MenuLink></li>
                </ul>
            </aside>

            {/* TODO: Add Mobile Support */}
            {/* <div className="dropdown is-hidden-tablet is-hoverable">
                <div className="dropdown-trigger">
                    <button className="button" aria-haspopup="true" aria-controls="dropdown-menu">
                    <span>Select Panel</span>
                    <span className="icon is-small">
                        <i className="fas fa-angle-down" aria-hidden="true"></i>
                    </span>
                    </button>
                </div>
                <div className="dropdown-menu" id="dropdown-menu" role="menu">
                    <div className="dropdown-content">
                    <a href="#" className="dropdown-item">
                        Dropdown item
                    </a>
                    <a className="dropdown-item">
                        Other dropdown item
                    </a>
                    <a href="#" className="dropdown-item">
                        Active dropdown item
                    </a>
                    <a href="#" className="dropdown-item">
                        Other dropdown item
                    </a>
                    <hr className="dropdown-divider"></hr>
                    <a href="#" className="dropdown-item">
                        With a divider
                    </a>
                    </div>
                </div>
            </div> */}
        </div>
    )
}

export {AdminMenu};