from gql import gql

QUERY = gql(
        """
        query {
            reportData {
                report(code:"XC3gvMtmALBKjWyz") {
                    events(fightIDs: [3]) {
                        data
                    }
                    startTime,
                    fights(fightIDs: [3]) {
                        friendlyPlayers
                    }
                    masterData {
                        actors {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
    )