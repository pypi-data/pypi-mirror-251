import Outline from "../components/Outline"
import { Column, Columns } from "../components/Columns"

export default function About() {
    return(
        <Outline>
        <Columns>
        <Column args={"is-6 is-offset-3"}>
            <div className="content">
                <h1 className="has-text-light">About: Fastapp</h1>
                <p>
                    Fastapp is a boilerplate fullstack application framework, utilizing fastapi and a sql database
                    for a backend and react with bulma for a frontend. This project is meant to be a starting point for
                    any fullstack application, and is meant to be as simple as possible to get up and running.
                </p>
                <h2 className="has-text-light">Features</h2>
                <Columns>
                    <Column args={'is-offset-1 is-4'}>
                        <ul>
                            <li>Fastapi Backend</li>
                            <li>React Frontend</li>
                            <li>SQL Database</li>
                            <li>Docker Development & Production Environments</li>
                        </ul>
                    </Column>
                    <Column args={'is-offset-1 is-4'}>
                        <ul>
                            <li>JWT OAuth2 Authentication</li>
                            <li>Administrator Panel</li>
                            <li>Simple User Management</li>
                            <li>CI/CD for Linting and Building/Tagging Docker Images</li>
                        </ul>
                    </Column>
                </Columns>
            </div>
        </Column>
        </Columns>
        </Outline>
    )
}