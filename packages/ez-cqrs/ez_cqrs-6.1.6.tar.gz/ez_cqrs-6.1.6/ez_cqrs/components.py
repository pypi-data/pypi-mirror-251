"""CQRS core components."""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, final

from typing_extensions import TypeVar

from ez_cqrs._typing import T

if TYPE_CHECKING:
    from result import Result


@final
@dataclass
class StateChanges(Generic[T]):
    """
    Operations registry.

    The intended use case for `StateChanges` is to act as an ephemeral
    record of update operations against a database in the execution of a command.

    These update operations would be commited as a single, ACID, transaction agains the
    database before the command execution returns the events recorded.
    """

    max_lenght: int
    _storage: list[T] = field(default_factory=list, init=False)

    def is_empty(self) -> bool:
        """Check `StateChanges` storage is empty."""
        return self.storage_length() == 0

    def add(self, value: T) -> None:
        """Add new value to the storage registry."""
        if len(self._storage) >= self.max_lenght:
            msg = "StateChanges capacity exceeded."
            raise RuntimeError(msg)
        self._storage.append(value)

    def prune_storage(self) -> None:
        """Prune storage."""
        self._storage.clear()

    def storage_snapshot(self) -> list[T]:
        """Get an snapshot of the storage."""
        return self._storage.copy()

    def storage_length(self) -> int:
        """Get storage length."""
        return len(self._storage)


class ACID(abc.ABC, Generic[T]):
    """
    Repository gives acces to the system database layer.

    A database must support transaction operations.

    Besides being the client between the core layer and the persistence layer,
    a system repository is intended to be used right before a command handling
    returns. Before events are returned to the client to be propagated to other
    systems, all update operations recorded during the command execution must be
    commited.
    """

    @abc.abstractmethod
    def commit_as_transaction(
        self,
        ops_registry: StateChanges[T],
    ) -> None:
        """
        Commit update operations stored in an `StateChanges`.

        The operation is executed as a transaction againts the database.

        After the commit the ops_registry must be pruned.
        """


class DomainError(Exception):
    """
    Raised when a user violates a business rule.

    This is the error returned when a user violates a business rule. The payload passed
    should be used to inform the user of the nature of a problem.

    This translates into a `Bad Request` status.
    """


@final
class UnexpectedError(Exception):
    """
    Raised when an unexpected error was encountered.

    A technical error was encountered teht prevented the command from being applied to
    the aggregate. In general the accompanying message should be logged for
    investigation rather than returned to the user.
    """

    def __init__(self, unexpected_error: Exception) -> None:  # noqa: D107
        super().__init__(f"Unexpected error {unexpected_error}")


@final
class TransactionExecutionError(Exception):
    """Error raised when the transaction execution fails."""

    def __init__(self, error: Exception) -> None:  # noqa: D107
        super().__init__(f"Failure while executing the transaction. Error: {error}")


@dataclass(frozen=True)
class BaseResponse:
    """Response container."""


@dataclass(frozen=True)
class IDomainEvent(abc.ABC):
    """
    Domain Event base class.

    A `IDomainEvent` represents any business change in the state of an `Aggregate`.
    `DomainEvents` are inmutable, and when [event sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
    is used they are the single source of truth.

    The name of a `IDomainEvent` should always be in the past tense, e.g.,
    - AdminPrivilegesGranted
    - EmailAddressChanged
    - DependencyAdded

    To simplify serialization, an event should be an enum, and each variant should carry
    any important information.
    """

    @abc.abstractmethod
    async def publish(self) -> None:
        """Define how to handle the event."""


R = TypeVar("R", bound=BaseResponse, covariant=False)
E = TypeVar("E", bound=IDomainEvent, covariant=False)


@dataclass(frozen=True)
class ICommand(Generic[E, R, T], abc.ABC):
    """
    ICommand baseclass.

    In order to make changes to our system we'll need commands. These
    are the simplest components of any CQRS system and consist of little more than
    packaged data.
    """

    @abc.abstractmethod
    async def execute(
        self,
        state_changes: StateChanges[T],
        events: list[E],
    ) -> Result[R, DomainError]:
        """Execute command."""
