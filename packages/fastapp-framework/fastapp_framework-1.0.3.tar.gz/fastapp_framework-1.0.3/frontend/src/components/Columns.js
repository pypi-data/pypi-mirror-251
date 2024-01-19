
const Column = (props) => {
    return (
        <div className={`column ${props.args}`}>
            {props.children}
        </div>
    )
}

const Columns = (props) => {
    return(
        <div className={`columns ${props.args}`}>
            {props.children}
        </div>
    )
}

export {Columns, Column};