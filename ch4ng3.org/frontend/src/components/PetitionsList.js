import React, { Component } from 'react'
import { connect } from 'react-redux'
import { getPetitions } from '../actions'
import { Button, Item, Segment } from 'semantic-ui-react'
import PetitionItem from './PetitionItem'

class PetitionsList extends Component {
  state = { isLoading: true }

  loadMore = () => {
    const { dispatch, petitions, filter } = this.props
    const currentPage = Math.floor(petitions.length / 10)
    dispatch(getPetitions({ ...filter, page: currentPage + 1 }))
  }

  componentWillReceiveProps(nextProps) {
    const { user, dispatch, filter } = this.props

    // Get petitions is user logged in/out
    if (user !== nextProps.user) {
      this.setState({ isLoading: true })
      dispatch(getPetitions(filter))
        .then(() => this.setState({ isLoading: false }))
    }
  }

  componentDidMount() {
    const { dispatch, filter } = this.props
    dispatch(getPetitions(filter))
      .then(() => this.setState({ isLoading: false }))
  }

  render() {
    const { petitions, user, emptyMessage } = this.props
    const { isLoading } = this.state

    return (
      <Segment basic={true} loading={isLoading}>
        { petitions.length > 0 ?
          <Item.Group divided>
            { petitions.map(
              (petition, i) => (
                <PetitionItem
                  key={i}
                  petition={petition}
                  isLoggedIn={user.id !== undefined}
                  isAuthor={user.id === petition.user_id}
                  {...this.props} />
              )
            )}

            { petitions.length % 10 === 0 ?
                <Button
                  onClick={this.loadMore}
                  color='red'
                  fluid>
                  Load more
                </Button>
                :
                null
            }
          </Item.Group>
          :
          <h3>{emptyMessage}</h3>
        }
      </Segment>
    )
  }
}

const mapStateToProps = (state) => {
  const { user, petitions } = state
  return {
    user,
    petitions
  }
}

export default connect(mapStateToProps)(PetitionsList)
