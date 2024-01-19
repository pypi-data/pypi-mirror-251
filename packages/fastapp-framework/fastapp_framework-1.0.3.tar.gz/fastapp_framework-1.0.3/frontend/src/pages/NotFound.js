import Outline from '../components/Outline';

import metadata from '../metadata';

export default function NotFound(){
    return (
        <Outline>
            <div>
                <h1 className='has-text-centered title'>Page Not Found</h1>
                <br></br>
                <h2 className='has-text-centered subtitle'>If you believe this is an error contact: {metadata.errorContact}</h2>
            </div>
        </Outline>
    )
}