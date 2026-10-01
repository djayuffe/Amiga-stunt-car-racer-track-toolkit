class SCRToolError(Exception): pass
class FormatError(SCRToolError): pass
class TruncatedError(FormatError): pass
class ValidationError(FormatError): pass
class EvidenceError(SCRToolError): pass
