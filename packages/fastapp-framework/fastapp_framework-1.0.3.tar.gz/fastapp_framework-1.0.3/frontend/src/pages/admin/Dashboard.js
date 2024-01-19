import {Column, Columns} from '../../components/Columns'

const StatBox = (props) => {
    return (
        <Column args={'is-3'}>
            <div className='box has-background-grey'>
                <p className='subtitle has-text-centered'>{props.name}</p>
                <hr></hr>
                <p className='title has-text-centered'>NUMBER</p>
            </div>
        </Column>
    )
}

export default function Dashboard(props){
    return (
        <div>
            <Columns>
                <StatBox name={'Statistic 1'}/>
                <StatBox name={'Statistic 2'}/>
                <StatBox name={'Statistic 3'}/>
                <StatBox name={'Statistic 4'}/>
            </Columns>
            <div className='box has-background-grey has-text-light'>
                MORE INFO
            </div>
        </div>
    )
}