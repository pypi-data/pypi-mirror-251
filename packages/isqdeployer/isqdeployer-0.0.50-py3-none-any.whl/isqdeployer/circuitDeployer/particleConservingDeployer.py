from .abcDeployer import BaseDeployer


class particleConservingError(Exception):
    pass


class Deployer(BaseDeployer):
    """
    target: isQ.particleConserving.isq


    """

    def _Preambles(self):
        return ["import isQLib.particleConserving as parConserGate;"]

    def G(self, qid1, qid0, theta):
        varName_theta = self.get_isqVarNameWithAppendIsQ(theta)
        varName_Q0 = f"Q[{self.qMap[qid0]}]"
        varName_Q1 = f"Q[{self.qMap[qid1]}]"
        self.circuit.appendCode(
            f"parConserGate.G( {varName_theta} , {varName_Q1}, {varName_Q0} ); "
        )
        return self

    def CG(self, ctlqid, qid1, qid0, theta):
        varName_theta = self.get_isqVarNameWithAppendIsQ(theta)
        varName_Q0 = f"Q[{self.qMap[qid0]}]"
        varName_Q1 = f"Q[{self.qMap[qid1]}]"
        varName_ctlqid = f"Q[{self.qMap[ctlqid]}]"
        self.circuit.appendCode(
            f"parConserGate.Control_G( {varName_theta} , {varName_ctlqid}, {varName_Q1}, {varName_Q0} ); "
        )
        return self

    def G2(self, qid3, qid2, qid1, qid0, theta):
        varName_theta = self.get_isqVarNameWithAppendIsQ(theta)
        varName_Q0 = f"Q[{self.qMap[qid0]}]"
        varName_Q1 = f"Q[{self.qMap[qid1]}]"
        varName_Q2 = f"Q[{self.qMap[qid2]}]"
        varName_Q3 = f"Q[{self.qMap[qid3]}]"
        self.circuit.appendCode(
            f"parConserGate.G2( {varName_theta} , {varName_Q3}, {varName_Q2}, {varName_Q1}, {varName_Q0} ); "
        )
        return self
