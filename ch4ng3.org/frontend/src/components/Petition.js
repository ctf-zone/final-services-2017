import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Accordion, Icon, Segment } from 'semantic-ui-react'
import PetitionSignatures from './PetitionSignatures'
import PetitionAuthor from './PetitionAuthor'
import { getPetition, getSigners } from '../actions'

class Petition extends Component {
  state = {
    isLoading: true,
    signersIsOpened: false
  }

  toggleSigners = () => {
    const { signersIsOpened } = this.state
    this.setState({
      signersIsOpened: !signersIsOpened
    })
  }

  onSign = () => {
    const { dispatch, match } = this.props

    this.setState({ isLoading: true })

    dispatch(getPetition(match.params.id))
      .then(() => this.setState({ isLoading: false }))

    dispatch(getSigners(match.params.id))
  }

  componentDidMount() {
    const { match, dispatch } = this.props
    dispatch(getPetition(match.params.id))
      .then(() => this.setState({ isLoading: false }))
    dispatch(getSigners(match.params.id))
  }

  render() {
    const { petition, signers } = this.props
    const { isLoading, signersIsOpened } = this.state

    return (
      <Segment
        style={{ minHeight: '100px' }}
        loading={isLoading}>
        { petition && !isLoading ?
          <div>
            <h1>{petition.title}</h1>
            <p>{petition.text}</p>

            <span>
              <PetitionAuthor
                petition={petition} />
            </span>

            <span style={{ marginLeft: '5px' }}>
              <PetitionSignatures
                onSign={this.onSign}
                petition={petition} />
            </span>
          </div>
          :
          null
        }
        <Accordion fluid style={{ marginTop: '20px' }}>
          <Accordion.Title
            active={signersIsOpened}
            index={0}
            onClick={this.toggleSigners}>

            <Icon name='dropdown' />
            Signers
          </Accordion.Title>

          <Accordion.Content
            active={signersIsOpened}>
            { signers.map(
              (signer, i) => <span key={i}>{ i === 0 ? '' : ', ' }{signer.name}</span>
            ) }
          </Accordion.Content>
        </Accordion>
      </Segment>
    )
  }
}

const mapStateToProps = (state) => {
  const { petition, signers } = state
  return {
    petition,
    signers
  }
}

export default connect(mapStateToProps)(Petition)
