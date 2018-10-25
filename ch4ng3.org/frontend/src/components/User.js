import React, { Component } from 'react'
import { connect } from 'react-redux'
import PetitionsList from './PetitionsList'
import { getUserById } from '../actions'

class User extends Component {

  componentDidMount() {
    const { dispatch, match } = this.props
    dispatch(getUserById(match.params.id))
  }

  render() {
    const { match, users } = this.props

    return (
      <div>
        <h1>{ `${users.name}'s petitions` }</h1>
        <PetitionsList
          emptyMessage='There are no petitions :('
          filter={{ author_id: match.params.id }} />
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  const { users } = state
  return {
    users
  }
}

export default connect(mapStateToProps)(User)
