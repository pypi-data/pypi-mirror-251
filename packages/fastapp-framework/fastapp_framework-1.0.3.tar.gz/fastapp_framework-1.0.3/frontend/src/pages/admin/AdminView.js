import { useState, useEffect } from "react"
import { useCookies } from "react-cookie"

import Outline from "../../components/Outline"
import { Column, Columns } from "../../components/Columns"
import { AdminMenu } from "../../components/Menu"
import Dashboard from "./Dashboard"
import Members from "./Members"
import AddUser from "./AddUser"

const views = {
    'Dashboard': <Dashboard />,
    'Members': <Members is_admin={false}/>,
    'Admins': <Members is_admin={true}/>,
    'Add Users': <AddUser />
}

export default function Admin(props){
    const [activeView, setActiveView] = useState('Dashboard')
    const [cookies, , ] = useCookies(['fastapp_token']);

    useEffect(() => {
        const isAdmin = (cookies.fastapp_token !== undefined) ? 
                        (cookies.fastapp_token.grants.find((value) => value === "admin") !== undefined) : false;
        if(!isAdmin){
            window.location.replace("/login")
        }
    }, [cookies.fastapp_token]);
    
    return(
        <Outline>
            <h2 className="title has-text-centered">Fastapp Administration</h2>
            <br></br>
            <Columns>
                <Column args={'is-2 ml-2'}>
                    <AdminMenu active={activeView} setActive={setActiveView}/>
                </Column>
                <Column args={'ml-4 mr-4'}>
                    {views[activeView]}
                </Column>
            </Columns>
        </Outline>
    )
}